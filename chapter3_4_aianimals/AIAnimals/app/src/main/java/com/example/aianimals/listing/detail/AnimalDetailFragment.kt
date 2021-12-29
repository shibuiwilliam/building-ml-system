package com.example.aianimals.listing.detail

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.example.aianimals.R
import com.example.aianimals.repository.Animal

class AnimalDetailFragment : Fragment(), AnimalDetailContract.View {
    override lateinit var presenter: AnimalDetailContract.Presenter

    private lateinit var animalImageView: ImageView
    private lateinit var animalNameView: TextView
    private lateinit var animalLikesView: TextView
    private lateinit var animalSubmitDateView: TextView
    private lateinit var animalDescriptionView: TextView

    override fun showAnimal(animal: Animal) {
        animalNameView.text = animal.name
        animalLikesView.text = animal.likes.toString()
        animalSubmitDateView.text = animal.date
        animalDescriptionView.text = animal.description

        animalNameView.visibility = View.VISIBLE
        animalLikesView.visibility = View.VISIBLE
        animalSubmitDateView.visibility = View.VISIBLE
        animalDescriptionView.visibility = View.VISIBLE

        Glide.with(this).load(animal.imageUrl).into(animalImageView)
        animalImageView.visibility = View.VISIBLE
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
            R.layout.animal_detail_fragment,
            container,
            false
        )

        with(root)
        {
            activity?.title = getString(R.string.animal_detail)

            animalImageView = findViewById(R.id.animal_image)
            animalNameView = findViewById(R.id.animal_name)
            animalLikesView = findViewById(R.id.animal_likes)
            animalSubmitDateView = findViewById(R.id.animal_submit_date)
            animalDescriptionView = findViewById(R.id.animal_description)
        }
        return root
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
