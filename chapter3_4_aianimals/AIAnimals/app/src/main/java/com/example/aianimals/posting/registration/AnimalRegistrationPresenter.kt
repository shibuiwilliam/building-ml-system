package com.example.aianimals.posting.registration

import android.util.Log
import com.example.aianimals.middleware.Utils
import com.example.aianimals.repository.Animal
import com.example.aianimals.repository.source.AnimalRepository
import java.text.SimpleDateFormat
import java.util.*

class AnimalRegistrationPresenter(
    private val imageUri: String?,
    private val animalRepository: AnimalRepository,
    private val animalRegistrationView: AnimalRegistrationContract.View
) : AnimalRegistrationContract.Presenter {
    private val TAG = AnimalRegistrationPresenter::class.java.simpleName

    init {
        this.animalRegistrationView.presenter = this
    }

    private var animalName: String? = null
    override fun getAnimalName(): String? {
        return animalName
    }

    override fun setAnimalName(value: String) {
        animalName = value
    }

    private var animalDescription: String? = null
    override fun getAnimalDescription(): String? {
        return animalDescription
    }

    override fun setAnimalDescription(value: String) {
        animalDescription = value
    }

    override fun getImageUri(): String? {
        return imageUri
    }

    override fun start() {
        if (animalName != null) {
            this.animalRegistrationView.setAnimalName(animalName!!)
        }
        if (animalDescription != null) {
            this.animalRegistrationView.setAnimalDescription(animalDescription!!)
        }
        showImage()
    }

    override fun showImage() {
        this.animalRegistrationView.showImage(imageUri)
    }

    override fun addAnimal(animal: Animal) {
        Log.i(TAG, "register ${animal}")
        animalRepository.saveAnimal(animal)
    }

    override fun makeAnimal(): Animal? {
        if (animalName == null || animalDescription == null || imageUri == null) {
            return null
        }
        val id = Utils.generateUUID()
        val now = Date()
        val today = SimpleDateFormat("yyyy/MM/dd").format(now).toString()
        return Animal(
            id,
            animalName!!,
            animalDescription!!,
            today,
            0,
            imageUri
        )
    }

    override fun clearCurrentValues() {
        animalName = null
        animalDescription=null
    }
}