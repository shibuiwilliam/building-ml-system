package com.example.aianimals.listing.listing

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.SearchView
import android.widget.Spinner
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.example.aianimals.R
import com.example.aianimals.listing.detail.AnimalDetailActivity
import com.example.aianimals.posting.registration.AnimalRegistrationActivity
import com.example.aianimals.repository.animal.Animal
import com.google.android.material.floatingactionbutton.FloatingActionButton

class AnimalListFragment : Fragment(), AnimalListContract.View {
    private val TAG = AnimalListFragment::class.java.simpleName

    override lateinit var presenter: AnimalListContract.Presenter

    private lateinit var animalListRecyclerViewAdapter: AnimalListRecyclerViewAdapter

    private lateinit var searchView: SearchView
    private lateinit var categorySpinner: Spinner
    private lateinit var subcategorySpinner: Spinner
    private lateinit var sortSpinner: Spinner
    private lateinit var swipeRefreshLayout: SwipeRefreshLayout
    private lateinit var animalRecyclerView: RecyclerView

    override fun showAnimals(animals: Map<String, Animal>) {
        searchView.visibility = View.VISIBLE
        animalListRecyclerViewAdapter.animals = animals.values.toMutableList()
        animalRecyclerView.visibility = View.VISIBLE
    }

    override fun appendAnimals(animals: Map<String, Animal>) {
        searchView.visibility = View.VISIBLE
        animalListRecyclerViewAdapter.animals.addAll(animals.values.toList())
        animalRecyclerView.visibility = View.VISIBLE
    }

    override fun onResume() {
        super.onResume()
        presenter.start()
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(
            R.layout.animal_list_fragment,
            container,
            false
        )

        with(root) {
            activity?.title = getString(R.string.animal_list)

            animalListRecyclerViewAdapter =
                AnimalListRecyclerViewAdapter(context, mutableMapOf(), presenter)

            searchView = findViewById(R.id.search_view)
            searchView.setOnQueryTextListener(
                object : SearchView.OnQueryTextListener {
                    override fun onQueryTextChange(newText: String?): Boolean {
                        if (newText == "") {
                            presenter.query = null
                        } else {
                            presenter.query = newText
                        }
                        return false
                    }

                    override fun onQueryTextSubmit(query: String?): Boolean {
                        presenter.listAnimals(query)
                        return true
                    }
                }
            )

            categorySpinner = findViewById(R.id.category_spinner)
            subcategorySpinner = findViewById(R.id.subcategory_spinner)
            sortSpinner = findViewById(R.id.sort_spinner)

            val categorySpinnerAdapter =
                ArrayAdapter(
                    context,
                    android.R.layout.simple_spinner_item,
                    presenter.animalCategories
                )
            val subcategorySpinnerAdapter =
                ArrayAdapter(
                    context,
                    android.R.layout.simple_spinner_item,
                    presenter.animalSubcategories
                )
            val sortSpinnerAdapter =
                ArrayAdapter(
                    context,
                    android.R.layout.simple_spinner_item,
                    presenter.sortValues
                )

            categorySpinner.adapter = categorySpinnerAdapter
            categorySpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                override fun onItemSelected(
                    parent: AdapterView<*>?,
                    view: View?,
                    position: Int,
                    id: Long
                ) {
                    val spinnerParent = parent as Spinner
                    presenter.selectedAnimalCategory = spinnerParent.selectedItem as String
                    presenter.loadAnimalSubcategory(presenter.selectedAnimalCategory, null)
                    presenter.listAnimals(presenter.query)
                }

                override fun onNothingSelected(parent: AdapterView<*>?) {}
            }

            subcategorySpinner.adapter = subcategorySpinnerAdapter
            subcategorySpinner.onItemSelectedListener =
                object : AdapterView.OnItemSelectedListener {
                    override fun onItemSelected(
                        parent: AdapterView<*>?,
                        view: View?,
                        position: Int,
                        id: Long
                    ) {
                        val spinnerParent = parent as Spinner
                        presenter.selectedAnimalSubcategory = spinnerParent.selectedItem as String
                        presenter.listAnimals(presenter.query)
                    }

                    override fun onNothingSelected(parent: AdapterView<*>?) {}
                }

            sortSpinner.adapter = sortSpinnerAdapter
            sortSpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
                override fun onItemSelected(
                    parent: AdapterView<*>?,
                    view: View?,
                    position: Int,
                    id: Long
                ) {
                    val spinnerParent = parent as Spinner
                    presenter.selectedSortValue = spinnerParent.selectedItem as String
                    presenter.listAnimals(presenter.query)
                }

                override fun onNothingSelected(parent: AdapterView<*>?) {}
            }

            swipeRefreshLayout = findViewById(R.id.swipe)
            swipeRefreshLayout.apply {
                setOnRefreshListener {
                    Handler(Looper.getMainLooper()).postDelayed(Runnable {
                        swipeRefreshLayout.isRefreshing = false
                        presenter.listAnimals(presenter.query)
                    }, 500)
                }
            }

            animalRecyclerView = findViewById<RecyclerView>(R.id.recycler_view).apply {
                adapter = animalListRecyclerViewAdapter
            }
            animalRecyclerView.layoutManager = GridLayoutManager(
                context,
                2,
                RecyclerView.VERTICAL,
                false
            )
//            animalRecyclerView.addOnScrollListener(
//                object : RecyclerView.OnScrollListener() {
//                    override fun onScrollStateChanged(
//                        recyclerView: RecyclerView,
//                        newState: Int
//                    ) {
//                            super.onScrollStateChanged(recyclerView, newState)
//                            if (recyclerView.canScrollVertically(1) && newState == RecyclerView.SCROLL_STATE_IDLE) {
//                            }
//                    }
//                }
//            )

            animalListRecyclerViewAdapter.setOnAnimalCellClickListener(
                object : AnimalListRecyclerViewAdapter.OnAnimalCellClickListener {
                    override fun onItemClick(animal: Animal) {
                        val intent = Intent(context, AnimalDetailActivity::class.java).apply {
                            putExtra(AnimalDetailActivity.EXTRA_ANIMAL_ID, animal.id)
                            putExtra(AnimalDetailActivity.EXTRA_QUERY_STRING, presenter.query)
                            putExtra(
                                AnimalDetailActivity.EXTRA_QUERY_ANIMAL_CATEGORY,
                                presenter.selectedAnimalCategory
                            )
                            putExtra(
                                AnimalDetailActivity.EXTRA_QUERY_ANIMAL_SUBCATEGORY,
                                presenter.selectedAnimalSubcategory
                            )
                        }
                        startActivity(intent)
                    }
                }
            )

            searchView.setQuery(presenter.query, true)
        }

        requireActivity().findViewById<FloatingActionButton>(R.id.add_animal_button).apply {
            setOnClickListener {
                val intent = Intent(context, AnimalRegistrationActivity::class.java)
                startActivity(intent)
            }
        }
        return root
    }

    companion object {
        fun newInstance(): AnimalListFragment {
            return AnimalListFragment()
        }
    }
}