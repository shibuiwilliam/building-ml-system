package com.example.aianimals.listing

import android.util.Log
import com.example.aianimals.repository.Animal
import com.example.aianimals.repository.source.AnimalDataSource
import com.example.aianimals.repository.source.AnimalRepository

class AnimalListPresenter(
    val animalRepository: AnimalRepository,
    val animalView: AnimalListContract.View
) : AnimalListContract.Presenter{
    init {
        this.animalView.presenter = this
    }

    override fun start() {
        listAnimals()
    }

    override fun listAnimals() {
        this.animalRepository.listAnimals(object : AnimalDataSource.ListAnimalsCallback{
            override fun onListAnimal(animals: Map<Int, Animal>) {
                animalView.showAddresses(animals)
            }
        })
    }
}