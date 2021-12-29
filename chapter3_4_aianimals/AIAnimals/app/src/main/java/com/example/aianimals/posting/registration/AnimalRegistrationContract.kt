package com.example.aianimals.posting.registration

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView
import com.example.aianimals.repository.Animal

interface AnimalRegistrationContract {
    interface Presenter : BasePresenter {
        fun showImage()
        fun addAnimal(animal: Animal)
        fun makeAnimal(
            animalName: String,
            animalDescription: String,
            animalImageUrl: String
        ): Animal
        fun getImageUri(): String?
    }

    interface View : BaseView<Presenter> {
        fun showImage(imageUri: String?)
        fun registerAnimal(animal: Animal)
        fun setAnimalName(animalName: String)
        fun setAnimalDescription(animalDescription: String)
    }
}
