package com.example.aianimals.listing.listing

import android.util.Log
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.access_log.AccessLog
import com.example.aianimals.repository.access_log.AccessLogAction
import com.example.aianimals.repository.access_log.source.AccessLogRepository
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.login.source.LoginRepository
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext

class AnimalListPresenter(
    private val animalRepository: AnimalRepository,
    private val loginRepository: LoginRepository,
    private val accessLogRepository: AccessLogRepository,
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
    override lateinit var selectedSortBy: String
    override var modelName: String? = null

    override var currentPosition: Int = 0

    override var searchID: String = ""

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
        val animals = mutableMapOf<String, Animal>()
        withContext(appExecutors.ioContext) {
            val animalCategoryNameEn =
                if (selectedAnimalCategory == "ALL") null else selectedAnimalCategory
            val animalSubcategoryNameEn =
                if (selectedAnimalSubcategory == "ALL") null else selectedAnimalSubcategory
            val response = animalRepository.listAnimals(
                animalCategoryNameEn,
                null,
                animalSubcategoryNameEn,
                null,
                this@AnimalListPresenter.query,
                this@AnimalListPresenter.selectedSortBy,
                this@AnimalListPresenter.currentPosition
            )
            response.animals.forEach { animals[it.id] = it }
            selectedSortBy = response.sortBy
            modelName = response.modelName
            searchID = response.searchID
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

    override fun loadSortValues() = runBlocking {
        sortValues.clear()
        withContext(appExecutors.ioContext) {
            val svs = animalRepository.listAnimalSearchSortKey()
            for (sv in svs) {
                sortValues.add(sv.name)
            }
        }
        selectedSortBy = "created_at"
    }

    override fun likeAnimal(animal: Animal) = runBlocking {
        animalRepository.likeAnimal(animal.id)

        val phrases: ArrayList<String> = ArrayList()
        if (this@AnimalListPresenter.query != null) {
            phrases.addAll(this@AnimalListPresenter.query!!.split("\\s".toRegex()))
        }

        var animalCategoryID: Int? = null
        var animalSubcategoryID: Int? = null
        withContext(appExecutors.ioContext) {
            if (selectedAnimalCategory != "ALL") {
                animalCategoryID =
                    animalRepository.getAnimalCategory(selectedAnimalCategory, null)?.id
            }
            if (selectedAnimalSubcategory != "ALL") {
                animalSubcategoryID =
                    animalRepository.getAnimalSubcategory(selectedAnimalSubcategory, null)?.id
            }
        }

        Log.i(
            TAG,
            "access log ${AccessLogAction.LIKE.str} animal_id ${animal.id} phrases $phrases animalCategoryID $animalCategoryID animalSubcategoryID $animalSubcategoryID"
        )

        accessLogRepository.createAccessLog(
            AccessLog(
                searchID,
                phrases,
                animalCategoryID,
                animalSubcategoryID,
                selectedSortBy,
                modelName,
                animal.id,
                AccessLogAction.LIKE.str
            )
        )
    }

    override fun logout() = runBlocking {
        withContext(appExecutors.ioContext) {
            loginRepository.logout()
        }
    }
}