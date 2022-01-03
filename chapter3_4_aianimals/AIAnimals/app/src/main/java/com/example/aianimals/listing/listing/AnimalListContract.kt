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
        var selectedSortValue: String
        fun listAnimals(query: String?)
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
    }
}