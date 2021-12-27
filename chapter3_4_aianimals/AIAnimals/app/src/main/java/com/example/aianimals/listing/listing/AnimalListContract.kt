package com.example.aianimals.listing.listing

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView
import com.example.aianimals.repository.Animal

interface AnimalListContract {
    interface Presenter : BasePresenter {
        fun listAnimals()
    }

    interface View: BaseView<Presenter> {
        fun showAnimals(animals: Map<Int, Animal>)
    }
}