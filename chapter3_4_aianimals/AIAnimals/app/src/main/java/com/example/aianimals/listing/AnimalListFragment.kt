package com.example.aianimals.listing

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.os.bundleOf
import androidx.fragment.app.Fragment
import androidx.fragment.app.setFragmentResult
import androidx.recyclerview.widget.DividerItemDecoration
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.aianimals.R
import com.example.aianimals.repository.Animal

class AnimalListFragment : Fragment(), AnimalListContract.View {
    override lateinit var presenter: AnimalListContract.Presenter
    private val animalListRecyclerViewAdapter = AnimalListRecyclerViewAdapter(mutableMapOf<Int, Animal>())
    private lateinit var animalListView: RecyclerView

    override fun showAddresses(animals: Map<Int, Animal>) {
        animalListRecyclerViewAdapter.animals = animals
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
        val root = inflater.inflate(R.layout.fragment_animal_list, container, false)

        with (root) {
            activity?.title = getString(R.string.item_list)
            animalListView = findViewById<RecyclerView>(R.id.recycler_view).apply { adapter=animalListRecyclerViewAdapter }
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
                        setFragmentResult(
                            "animalData",
                            bundleOf(
                                "animalName" to animal.name,
                                "animalPrice" to animal.price,
                                "animalPurchaseDate" to animal.date
                            )
                        )
                        parentFragmentManager
                            .beginTransaction()
                            .replace(R.id.flagment_activity_main, AnimalFragment())
                            .addToBackStack(null)
                            .commit()
                    }
                }
            )
        }
        return root
    }

    companion object {
        fun newInstance(): AnimalListFragment{
            return AnimalListFragment()
        }
    }
}