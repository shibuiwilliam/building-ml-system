package com.example.aianimals.posting.registration

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.fragment.app.Fragment
import com.example.aianimals.R
import com.example.aianimals.listing.detail.AnimalDetailActivity
import com.example.aianimals.posting.camera.CameraActivity
import com.example.aianimals.repository.Animal
import com.google.android.material.floatingactionbutton.FloatingActionButton

class AnimalRegistrationFragment : Fragment(), AnimalRegistrationContract.View {
    override lateinit var presenter: AnimalRegistrationContract.Presenter

    private lateinit var registrationImageView: ImageView
    private lateinit var takePhotoButton: Button
    private lateinit var animalNameEdit: TextView
    private lateinit var animalDescriptionEdit: TextView

    private var imageUri: String? = null

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

            if (imageUri == null) {
                registrationImageView.setImageResource(R.mipmap.ic_launcher)
            }

            takePhotoButton.apply{
                setOnClickListener {
                    val intent = Intent(context, CameraActivity::class.java)
                    startActivity(intent)
                }
            }

            activity?.findViewById<FloatingActionButton>(R.id.add_animal_button)?.apply {
                setOnClickListener {
                    val animal = presenter.makeAnimal(
                        animalNameEdit.text.toString(),
                        animalDescriptionEdit.text.toString(),
                        "https://www.anicom-sompo.co.jp/nekonoshiori/wp-content/uploads/2018/12/724-2.jpg"
                    )
                    registerAnimal(animal)

                    val intent = Intent(context, AnimalDetailActivity::class.java).apply {
                        putExtra(AnimalDetailActivity.EXTRA_ANIMAL_ID, animal.id)
                    }
                    startActivity(intent)
                }
            }
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
        fun newInstance() = AnimalRegistrationFragment()
    }
}