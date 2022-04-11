package com.example.aianimals.listing.detail

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.activity.OnBackPressedCallback
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.aianimals.R
import com.example.aianimals.listing.listing.AnimalListActivity
import com.example.aianimals.repository.animal.Animal
import com.google.android.material.floatingactionbutton.ExtendedFloatingActionButton

class AnimalDetailFragment : Fragment(), AnimalDetailContract.View {
    private val TAG = AnimalDetailFragment::class.java.simpleName

    override lateinit var presenter: AnimalDetailContract.Presenter

    private lateinit var similarAnimalRecyclerViewAdapter: SimilarAnimalRecyclerViewAdapter

    private lateinit var animalImageView: ImageView
    private lateinit var animalNameView: TextView
    private lateinit var animalSubmitDateView: TextView
    private lateinit var animalDescriptionView: TextView
    private lateinit var animalLikeButton: ExtendedFloatingActionButton
    private lateinit var similarAnimalsView: RecyclerView

    override fun showAnimal(animal: Animal) {
        animalNameView.text = animal.name
        animalSubmitDateView.text = animal.date
        animalDescriptionView.text = animal.description

        animalNameView.visibility = View.VISIBLE
        animalSubmitDateView.visibility = View.VISIBLE
        animalDescriptionView.visibility = View.VISIBLE

        Glide.with(this).load(animal.imageUrl).into(animalImageView)
        animalImageView.visibility = View.VISIBLE
        animalLikeButton.text = animal.like.toString()

        val similarAnimals = presenter.searchSimilarAnimal()
        similarAnimalRecyclerViewAdapter.animals = similarAnimals.values.toMutableList()
        similarAnimalsView.visibility = View.VISIBLE
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(
            R.layout.animal_detail_fragment,
            container,
            false
        )

        with(root)
        {
            activity?.title = getString(R.string.animal_detail)

            similarAnimalRecyclerViewAdapter =
                SimilarAnimalRecyclerViewAdapter(context, mutableMapOf(), presenter)

            animalImageView = findViewById(R.id.animal_image)
            animalNameView = findViewById(R.id.animal_name)
            animalSubmitDateView = findViewById(R.id.animal_submit_date)
            animalDescriptionView = findViewById(R.id.animal_description)
            animalLikeButton = findViewById(R.id.animal_likes_button)

            requireActivity().onBackPressedDispatcher.addCallback(
                viewLifecycleOwner,
                object : OnBackPressedCallback(true) {
                    override fun handleOnBackPressed() {
                        val intent = Intent(context, AnimalListActivity::class.java)
                        presenter.stayLong(presenter.animal!!)
                        startActivity(intent)
                    }
                }
            )

            animalLikeButton.setOnClickListener {
                presenter.likeAnimal(presenter.animal!!)
            }

            similarAnimalsView = findViewById<RecyclerView>(R.id.similar_animals_view).apply {
                adapter = similarAnimalRecyclerViewAdapter
            }
            similarAnimalsView.layoutManager = GridLayoutManager(
                context,
                1,
                RecyclerView.HORIZONTAL,
                false
            )

            similarAnimalRecyclerViewAdapter.setOnAnimalCellClickListener(
                object : SimilarAnimalRecyclerViewAdapter.OnAnimalCellClickListener {
                    override fun onItemClick(animal: Animal) {
                        val intent = Intent(context, AnimalDetailActivity::class.java).apply {
                            putExtra(AnimalDetailActivity.EXTRA_ANIMAL_ID, animal.id)
                            putExtra(AnimalDetailActivity.EXTRA_QUERY_STRING, "image_search")
                            putExtra(
                                AnimalDetailActivity.EXTRA_QUERY_ANIMAL_CATEGORY,
                                "ALL"
                            )
                            putExtra(
                                AnimalDetailActivity.EXTRA_QUERY_ANIMAL_SUBCATEGORY,
                                "ALL"
                            )
                        }
                        startActivity(intent)
                    }
                }
            )
        }
        return root
    }

    override fun onResume() {
        super.onResume()
        presenter.start()
    }

    companion object {
        private val ARGUMENT_ANIMAL_ID = "ANIMAL_ID"

        fun newInstance(animalID: String?) = AnimalDetailFragment().apply {
            arguments = Bundle().apply {
                putString(ARGUMENT_ANIMAL_ID, animalID)
            }
        }
    }
}
