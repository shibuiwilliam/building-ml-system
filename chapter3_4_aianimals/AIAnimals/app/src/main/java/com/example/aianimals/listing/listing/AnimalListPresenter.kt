package com.example.aianimals.listing.listing

import android.util.Log
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalDataSource
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.login.source.LoginRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext
import kotlin.coroutines.CoroutineContext

class AnimalListPresenter(
    private val animalRepository: AnimalRepository,
    private val loginRepository: LoginRepository,
    private val animalListView: AnimalListContract.View,
    private val context: CoroutineContext = Dispatchers.Default
) : AnimalListContract.Presenter {
    private val TAG = AnimalListPresenter::class.java.simpleName

    init {
        this.animalListView.presenter = this
    }

    override fun start() {
        listAnimals()
    }

    override fun listAnimals()= runBlocking {
        withContext(context){
            val login = loginRepository.isLoggedIn()
            if (login != null){
                val token = login.token!!
                Log.i(TAG, "token: ${token}")
                val metadata = animalRepository.getMetadata(token)
                Log.i(TAG, "metadata: ${metadata}")
            }
            animalRepository.listAnimals(object : AnimalDataSource.ListAnimalsCallback {
                override fun onListAnimal(animals: Map<String, Animal>) {
                    animalListView.showAnimals(animals)
                }

                override fun onDataNotAvailable() {
                }
            })
        }
    }

    override fun logout() = runBlocking {
        withContext(context) {
            loginRepository.logout()
        }
    }
}