package com.example.aianimals.posting

import com.example.aianimals.middleware.Utils
import com.example.aianimals.repository.Animal
import com.example.aianimals.repository.source.AnimalRepository
import java.text.SimpleDateFormat
import java.util.*

class AnimalRegistrationPresenter(
    private val animalRepository: AnimalRepository,
    private val animalRegistrationView: AnimalRegistrationContract.View
) : AnimalRegistrationContract.Presenter {
    init {
        this.animalRegistrationView.presenter = this
    }

    override fun start() {
    }

    override fun addAnimal(animal: Animal) {
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
}