package com.example.aianimals.posting.registration

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.fragment.app.Fragment
import com.bumptech.glide.Glide
import com.example.aianimals.R
import com.example.aianimals.listing.detail.AnimalDetailActivity
import com.example.aianimals.listing.listing.AnimalListActivity
import com.example.aianimals.posting.camera.CameraActivity
import com.example.aianimals.repository.Animal
import com.google.android.material.floatingactionbutton.FloatingActionButton

class AnimalRegistrationFragment : Fragment(), AnimalRegistrationContract.View {
    private val TAG = AnimalRegistrationFragment::class.java.simpleName

    override lateinit var presenter: AnimalRegistrationContract.Presenter

    private lateinit var registrationImageView: ImageView
    private lateinit var takePhotoButton: Button
    private lateinit var animalNameEdit: TextView
    private lateinit var animalDescriptionEdit: TextView

    override fun showImage(imageUri: String?) {
        if (imageUri == null) {
            registrationImageView.setImageResource(R.mipmap.ic_launcher)
        } else {
            Glide.with(this).load(imageUri).into(registrationImageView)
        }

        registrationImageView.visibility = View.VISIBLE
    }

    override fun registerAnimal(animal: Animal) {
        presenter.addAnimal(animal)
    }

    override fun onResume() {
        super.onResume()
        presenter.start()
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val root = inflater.inflate(
            R.layout.animal_registration_fragment,
            container,
            false
        )

        with(root) {
            activity?.title = getString(R.string.animal_registration)

            registrationImageView = findViewById(R.id.registration_image)
            takePhotoButton = findViewById(R.id.take_photo_button)
            animalNameEdit = findViewById(R.id.animal_name_edit)
            animalDescriptionEdit = findViewById(R.id.animal_description_edit)

            takePhotoButton.apply {
                setOnClickListener {
                    val intent = Intent(context, CameraActivity::class.java)
                    startActivity(intent)
                }
            }

            activity?.findViewById<FloatingActionButton>(R.id.add_animal_button)?.apply {
                setOnClickListener {
                    val imageUri = presenter.getImageUri()
                    if (imageUri == null) {
                        Toast.makeText(
                            requireContext(),
                            "you must register photo",
                            Toast.LENGTH_SHORT
                        ).show()
                        Log.e(TAG, "you must register photo")
                    }
                    val animal = presenter.makeAnimal(
                        animalNameEdit.text.toString(),
                        animalDescriptionEdit.text.toString(),
                        imageUri!!
                    )
                    registerAnimal(animal)

                    val intent = Intent(context, AnimalDetailActivity::class.java).apply {
                        putExtra(AnimalDetailActivity.EXTRA_ANIMAL_ID, animal.id)
                    }
                    startActivity(intent)
                }
            }

            requireActivity().onBackPressedDispatcher.addCallback(
                this@AnimalRegistrationFragment,
                object : OnBackPressedCallback(true) {
                    override fun handleOnBackPressed() {
                        val intent = Intent(context, AnimalListActivity::class.java)
                        startActivity(intent)
                    }
                })
        }

        return root
    }

    override fun setAnimalName(animalName: String) {
        this.animalNameEdit.text = animalName
    }

    override fun setAnimalDescription(animalDescription: String) {
        this.animalDescriptionEdit.text = animalDescription
    }

    companion object {
        private val ARGUMENT_IMAGE_URI: String? = null

        fun newInstance(imageUri: String?) = AnimalRegistrationFragment().apply {
            arguments = Bundle().apply {
                putString(ARGUMENT_IMAGE_URI, imageUri)
            }
        }
    }
}