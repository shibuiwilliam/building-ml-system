package com.example.aianimals.listing.detail

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView
import com.example.aianimals.repository.animal.Animal

class AnimalDetailContract {
    interface Presenter : BasePresenter {
        fun getAnimal(animalID: String)
    }

    interface View : BaseView<Presenter> {
        fun showAnimal(animal: Animal)
    }
}