package com.example.aianimals.listing.detail

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView
import com.example.aianimals.repository.animal.Animal

class AnimalDetailContract {
    interface Presenter : BasePresenter {
        var animal: Animal?
        var queryString: String?
        var queryAnimalCategory: String
        var queryAnimalSubcategory: String
        var startTime: Long

        fun getAnimal(animalID: String)
        fun likeAnimal(animal: Animal)
        fun stayLong(animal: Animal)
        fun logout()
    }

    interface View : BaseView<Presenter> {
        fun showAnimal(animal: Animal)
    }
}