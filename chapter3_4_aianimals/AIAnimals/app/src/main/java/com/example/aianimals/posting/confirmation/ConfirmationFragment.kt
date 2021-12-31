package com.example.aianimals.posting.confirmation

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.example.aianimals.R
import com.example.aianimals.repository.animal.Animal

class ConfirmationFragment : Fragment(), ConfirmationContract.View {
    override lateinit var presenter: ConfirmationContract.Presenter

    private lateinit var animalImageView: ImageView
    private lateinit var animalNameView: TextView
    private lateinit var animalDescriptionView: TextView
    private lateinit var confirmationButton: Button
    private lateinit var cancellationButton: Button

    override fun showAnimal(animal: Animal) {
        Glide.with(this).load(animal.imageUrl).into(animalImageView)
        animalNameView.text = animal.name
        animalDescriptionView.text = animal.description

        animalImageView.visibility = View.VISIBLE
        animalNameView.visibility = View.VISIBLE
        animalDescriptionView.visibility = View.VISIBLE
        confirmationButton.visibility = View.VISIBLE
        cancellationButton.visibility = View.VISIBLE
    }

    override fun confirmRegistration(animal: Animal) {
    }

    override fun cancelRegistration() {
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(
            R.layout.confirmation_fragment,
            container,
            false
        )

        with(root) {
            animalImageView = findViewById(R.id.animal_image)
            animalNameView = findViewById(R.id.animal_name)
            animalDescriptionView = findViewById(R.id.animal_description)
            confirmationButton = findViewById(R.id.confirmation_button)
            cancellationButton = findViewById(R.id.cancellation_button)

        }
        return root
    }

    override fun onResume() {
        super.onResume()
        presenter.start()
    }

    companion object {
        fun newInstance() = ConfirmationFragment()
    }
}