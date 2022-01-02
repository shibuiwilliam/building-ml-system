package com.example.aianimals.listing.listing

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView
import com.example.aianimals.repository.animal.Animal

interface AnimalListContract {
    interface Presenter : BasePresenter {
        var token: String?
        var query: String?
        fun listAnimals(
            query: String?,
            refresh: Boolean
        )
        fun setToken()
        fun logout()
    }

    interface View : BaseView<Presenter> {
        fun showAnimals(animals: Map<String, Animal>)
    }
}