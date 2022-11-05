package com.example.aianimals.listing.listing

import com.example.aianimals.BasePresenter
import com.example.aianimals.BaseView
import com.example.aianimals.repository.animal.Animal

interface AnimalListContract {
    interface Presenter : BasePresenter {
        var query: String?
        var animalCategories: MutableList<String>
        var animalSubcategories: MutableList<String>
        var sortValues: MutableList<String>
        var selectedAnimalCategory: String
        var selectedAnimalSubcategory: String
        var selectedSortBy: String
        var modelName: String?
        var currentPosition: Int

        var searchID: String

        fun searchAnimals(): Map<String, Animal>
        fun listAnimals(query: String?)
        fun appendAnimals()
        fun loadAnimalMetadata(refresh: Boolean)
        fun loadAnimalCategory()
        fun loadAnimalSubcategory(
            animalCategoryNameEn: String?,
            animalCategoryNameJa: String?
        )

        fun loadSortValues()
        fun likeAnimal(animal: Animal)
        fun logout()
    }

    interface View : BaseView<Presenter> {
        fun showAnimals(animals: Map<String, Animal>)
        fun appendAnimals(animals: Map<String, Animal>)
    }
}