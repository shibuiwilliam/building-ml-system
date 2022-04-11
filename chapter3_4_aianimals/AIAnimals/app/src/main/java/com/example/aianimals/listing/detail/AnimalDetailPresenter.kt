package com.example.aianimals.listing.detail

import android.util.Log
import com.example.aianimals.middleware.AppExecutors
import com.example.aianimals.repository.access_log.AccessLog
import com.example.aianimals.repository.access_log.AccessLogAction
import com.example.aianimals.repository.access_log.source.AccessLogRepository
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.AnimalCategory
import com.example.aianimals.repository.animal.AnimalSubcategory
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.login.source.LoginRepository
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext

class AnimalDetailPresenter(
    private val animalID: String,
    private val animalRepository: AnimalRepository,
    private val loginRepository: LoginRepository,
    private val accessLogRepository: AccessLogRepository,
    private val animalDetailView: AnimalDetailContract.View,
    private val appExecutors: AppExecutors = AppExecutors()
) : AnimalDetailContract.Presenter {
    private val TAG = AnimalDetailPresenter::class.java.simpleName

    override var animal: Animal? = null
    override var queryString: String? = null
    override var queryAnimalCategory: String = "ALL"
    override var queryAnimalSubcategory: String = "ALL"
    override var startTime: Long = 0L

    private var phrases: ArrayList<String> = ArrayList()
    private var animalCategory: AnimalCategory? = null
    private var animalSubcategory: AnimalSubcategory? = null

    init {
        this.animalDetailView.presenter = this
        this.startTime = System.currentTimeMillis()
    }

    override fun start() {
        formatQuery()
        showAnimal()
    }

    override fun showAnimal() = runBlocking {
        withContext(appExecutors.ioContext) {
            animal = animalRepository.getAnimal(animalID)
        }
        if (animal != null) {
            Log.i(
                TAG,
                "access log ${AccessLogAction.SELECT.str} animal_id ${animal!!.id} phrases $queryString animalCategoryID $queryAnimalCategory animalSubcategoryID $queryAnimalSubcategory"
            )

            accessLogRepository.createAccessLog(
                AccessLog(
                    phrases,
                    animalCategory?.id,
                    animalSubcategory?.id,
                    animalID,
                    AccessLogAction.SELECT.str
                )
            )

            animalDetailView.showAnimal(animal!!)
        }
    }

    override fun searchSimilarAnimal(): Map<String, Animal> = runBlocking {
        var similarAnimals = mapOf<String, Animal>()
        withContext(appExecutors.ioContext) {
            similarAnimals = animalRepository.searchAnimalsByImage(animal!!.id)
        }
        return@runBlocking similarAnimals
    }

    override fun likeAnimal(animal: Animal) = runBlocking {
        animalRepository.likeAnimal(animal.id)

        Log.i(
            TAG,
            "access log ${AccessLogAction.LIKE.str} animal_id ${animal.id} phrases $queryString animalCategoryID $queryAnimalCategory animalSubcategoryID $queryAnimalSubcategory"
        )

        accessLogRepository.createAccessLog(
            AccessLog(
                this@AnimalDetailPresenter.phrases,
                this@AnimalDetailPresenter.animalCategory?.id,
                this@AnimalDetailPresenter.animalSubcategory?.id,
                animal.id,
                AccessLogAction.LIKE.str
            )
        )
    }

    override fun stayLong(animal: Animal) = runBlocking {
        val endTime = System.currentTimeMillis()
        val elapsedTime = endTime - startTime
        Log.i(TAG, "elapsed time: $elapsedTime millisecond")
        if (elapsedTime > 10 * 1000) {
            Log.i(
                TAG,
                "access log ${AccessLogAction.SEE_LONG.str} animal_id ${animal.id} phrases $queryString animalCategoryID $queryAnimalCategory animalSubcategoryID $queryAnimalSubcategory"
            )

            accessLogRepository.createAccessLog(
                AccessLog(
                    this@AnimalDetailPresenter.phrases,
                    this@AnimalDetailPresenter.animalCategory?.id,
                    this@AnimalDetailPresenter.animalSubcategory?.id,
                    animal.id,
                    AccessLogAction.SEE_LONG.str
                )
            )
        }
    }

    private fun formatQuery() = runBlocking {
        this@AnimalDetailPresenter.phrases.clear()
        if (this@AnimalDetailPresenter.queryString != null) {
            this@AnimalDetailPresenter.phrases.addAll(
                this@AnimalDetailPresenter.queryString!!.split(
                    "\\s".toRegex()
                )
            )
        }

        withContext(appExecutors.ioContext) {
            if (this@AnimalDetailPresenter.queryAnimalCategory != "ALL") {
                this@AnimalDetailPresenter.animalCategory = animalRepository.getAnimalCategory(
                    this@AnimalDetailPresenter.queryAnimalCategory,
                    null
                )
            }

            if (this@AnimalDetailPresenter.queryAnimalSubcategory != "ALL") {
                this@AnimalDetailPresenter.animalSubcategory =
                    animalRepository.getAnimalSubcategory(
                        this@AnimalDetailPresenter.queryAnimalSubcategory,
                        null
                    )
            }
        }

        Log.i(
            TAG,
            "Query phrases ${this@AnimalDetailPresenter.phrases} animalCategory ${this@AnimalDetailPresenter.animalCategory} animalSubcategory ${this@AnimalDetailPresenter.animalSubcategory}"
        )
    }

    override fun logout() = runBlocking {
        withContext(appExecutors.defaultContext) {
            loginRepository.logout()
        }
    }
}