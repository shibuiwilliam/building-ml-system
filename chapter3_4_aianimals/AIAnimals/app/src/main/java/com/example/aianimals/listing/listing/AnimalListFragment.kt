package com.example.aianimals.listing.listing

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.example.aianimals.R
import com.example.aianimals.listing.detail.AnimalDetailActivity
import com.example.aianimals.posting.registration.AnimalRegistrationActivity
import com.example.aianimals.repository.Animal
import com.google.android.material.floatingactionbutton.FloatingActionButton

class AnimalListFragment : Fragment(), AnimalListContract.View {
    private val TAG = AnimalListFragment::class.java.simpleName

    override lateinit var presenter: AnimalListContract.Presenter

    private val animalListRecyclerViewAdapter =
        AnimalListRecyclerViewAdapter(mutableMapOf())

    private lateinit var swipeRefreshLayout: SwipeRefreshLayout
    private lateinit var animalListView: RecyclerView

    override fun showAnimals(animals: Map<String, Animal>) {
        animalListRecyclerViewAdapter.animals = animals.values.toList()
        animalListView.visibility = View.VISIBLE
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

            swipeRefreshLayout = findViewById(R.id.swipe)
            swipeRefreshLayout.apply {
                setOnRefreshListener {
                    Handler(Looper.getMainLooper()).postDelayed(Runnable {
                        swipeRefreshLayout.isRefreshing = false
                        presenter.listAnimals()
                    }, 500)
                }
            }

            animalListView = findViewById<RecyclerView>(R.id.recycler_view).apply {
                adapter = animalListRecyclerViewAdapter
            }

            val linearLayoutManager = LinearLayoutManager(context)
            animalListView.layoutManager = linearLayoutManager
            animalListView.addItemDecoration(
                DividerItemDecoration(
                    context,
                    linearLayoutManager.orientation
                )
            )

            animalListRecyclerViewAdapter.setOnAnimalCellClickListener(
                object : AnimalListRecyclerViewAdapter.OnAnimalCellClickListener {
                    override fun onItemClick(animal: Animal) {
                        val intent = Intent(context, AnimalDetailActivity::class.java).apply {
                            putExtra(AnimalDetailActivity.EXTRA_ANIMAL_ID, animal.id)
                        }
                        startActivity(intent)
                    }
                }
            )
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