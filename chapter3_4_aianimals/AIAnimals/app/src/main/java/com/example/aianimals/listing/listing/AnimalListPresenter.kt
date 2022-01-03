package com.example.aianimals.listing.listing

import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.login.source.LoginRepository
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext

class AnimalListPresenter(
    private val animalRepository: AnimalRepository,
    private val loginRepository: LoginRepository,
    private val animalListView: AnimalListContract.View,
    private val appExecutors: AppExecutors = AppExecutors()
) : AnimalListContract.Presenter {
    private val TAG = AnimalListPresenter::class.java.simpleName

    override var query: String? = null
    override var animalCategories: MutableList<String> = mutableListOf()
    override var animalSubcategories: MutableList<String> = mutableListOf()
    override var sortValues: MutableList<String> = mutableListOf()

    override lateinit var selectedAnimalCategory: String
    override lateinit var selectedAnimalSubcategory: String
    override lateinit var selectedSortValue: String

    override var currentPosition: Int = 0

    init {
        this.animalListView.presenter = this
        loadAnimalMetadata(true)
        loadAnimalCategory()
        loadAnimalSubcategory(null, null)
        loadSortValues()
    }

    override fun start() {
        listAnimals(query)
    }

    override fun searchAnimals(): Map<String, Animal> = runBlocking {
        var animals = mapOf<String, Animal>()
        withContext(appExecutors.ioContext) {
            val animalCategoryNameEn =
                if (selectedAnimalCategory == "ALL") null else selectedAnimalCategory
            val animalSubcategoryNameEn =
                if (selectedAnimalSubcategory == "ALL") null else selectedAnimalSubcategory
            animals = animalRepository.listAnimals(
                animalCategoryNameEn,
                null,
                animalSubcategoryNameEn,
                null,
                this@AnimalListPresenter.query,
                this@AnimalListPresenter.currentPosition
            )
        }
        return@runBlocking animals
    }

    override fun listAnimals(query: String?) = runBlocking {
        this@AnimalListPresenter.currentPosition = 0
        this@AnimalListPresenter.query = query
        val animals = searchAnimals()
        currentPosition = animals.size
        animalListView.showAnimals(animals)
    }

    override fun appendAnimals() {
        val animals = searchAnimals()
        if (animals.isEmpty()) {
            return
        }
        currentPosition += animals.size
        animalListView.appendAnimals(animals)
    }

    override fun loadAnimalMetadata(refresh: Boolean) = runBlocking {
        animalRepository.loadAnimalMetadata(refresh)
    }

    override fun loadAnimalCategory() = runBlocking {
        animalCategories.clear()
        animalCategories.add("ALL")
        withContext(appExecutors.ioContext) {
            val cs = animalRepository.listAnimalCategory()
            for (c in cs) {
                animalCategories.add(c.nameEn)
            }
        }
        selectedAnimalCategory = "ALL"
    }

    override fun loadAnimalSubcategory(
        animalCategoryNameEn: String?,
        animalCategoryNameJa: String?
    ) = runBlocking {
        animalSubcategories.clear()
        animalSubcategories.add("ALL")
        withContext(appExecutors.ioContext) {
            val scs =
                animalRepository.listAnimalSubcategory(animalCategoryNameEn, animalCategoryNameJa)
            for (sc in scs) {
                animalSubcategories.add(sc.nameEn)
            }
        }
        selectedAnimalSubcategory = "ALL"
    }

    override fun loadSortValues() {
        sortValues.add("Newest")
        sortValues.add("Liked")
        sortValues.add("AI")
        selectedSortValue = "Newest"
    }

    override fun likeAnimal(animal: Animal) = runBlocking {
        animalRepository.likeAnimal(animal.id)
    }

    override fun logout() = runBlocking {
        withContext(appExecutors.ioContext) {
            loginRepository.logout()
        }
    }
}