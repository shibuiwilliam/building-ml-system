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

    override fun start() {
        showImage()
    }

    override fun showImage() {
        this.animalRegistrationView.showImage(imageUri)
    }

    override fun addAnimal(animal: Animal) {
        Log.i(TAG, "register ${animal}")
        animalRepository.saveAnimal(animal)
    }

    override fun makeAnimal(
        animalName: String,
        animalDescription: String,
        animalImageUrl: String
    ): Animal {
        val id = Utils.generateUUID()
        val now = Date()
        val today = SimpleDateFormat("yyyy/MM/dd").format(now).toString()
        return Animal(
            id,
            animalName,
            animalDescription,
            today,
            0,
            animalImageUrl
        )
    }

    override fun getImageUri(): String? {
        return imageUri
    }
}