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
import com.bumptech.glide.Glide
import com.example.aianimals.R
import com.example.aianimals.listing.listing.AnimalListActivity
import com.example.aianimals.repository.animal.Animal
import com.google.android.material.floatingactionbutton.ExtendedFloatingActionButton

class AnimalDetailFragment : Fragment(), AnimalDetailContract.View {
    override lateinit var presenter: AnimalDetailContract.Presenter

    private lateinit var animalImageView: ImageView
    private lateinit var animalNameView: TextView
    private lateinit var animalLikesView: TextView
    private lateinit var animalSubmitDateView: TextView
    private lateinit var animalDescriptionView: TextView
    private lateinit var animalLikeButton: ExtendedFloatingActionButton

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
        animalLikeButton.text = animal.likes.toString()
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
            animalLikeButton = findViewById(R.id.animal_likes_button)

            requireActivity().onBackPressedDispatcher.addCallback(
                this@AnimalDetailFragment,
                object : OnBackPressedCallback(true) {
                    override fun handleOnBackPressed() {
                        val intent = Intent(context, AnimalListActivity::class.java)
                        startActivity(intent)
                    }
                }
            )

            animalLikeButton.setOnClickListener {
                presenter.likeAnimal(presenter.animal!!)
            }
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
