package com.example.aianimals.posting.registration

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView
import com.example.aianimals.repository.Animal

interface AnimalRegistrationContract {
    interface Presenter : BasePresenter {
        fun getAnimalName(): String?
        fun setAnimalName(value: String)
        fun getAnimalDescription(): String?
        fun setAnimalDescription(value: String)
        fun getImageUri(): String?
        fun showImage()
        fun addAnimal(animal: Animal)
        fun makeAnimal(): Animal?
        fun clearCurrentValues()
    }

    interface View : BaseView<Presenter> {
        fun showImage(imageUri: String?)
        fun registerAnimal()
        fun setAnimalName(animalName: String)
        fun setAnimalDescription(animalDescription: String)
        fun saveCurrentValues()
    }
}
