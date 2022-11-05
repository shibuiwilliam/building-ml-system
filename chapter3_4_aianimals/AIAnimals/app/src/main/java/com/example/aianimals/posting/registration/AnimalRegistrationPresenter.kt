package com.example.aianimals.posting.registration

import android.util.Log
import android.widget.Toast
import com.example.aianimals.middleware.Utils
import com.example.aianimals.repository.animal.Animal
import com.example.aianimals.repository.animal.source.AnimalRepository
import com.example.aianimals.repository.login.source.LoginRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.runBlocking
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.*
import kotlin.coroutines.CoroutineContext

class AnimalRegistrationPresenter(
    private val photoUrl: String?,
    private val animalRepository: AnimalRepository,
    private val loginRepository: LoginRepository,
    private val animalRegistrationView: AnimalRegistrationContract.View,
    private val context: CoroutineContext = Dispatchers.Default
) : AnimalRegistrationContract.Presenter {
    private val TAG = AnimalRegistrationPresenter::class.java.simpleName
    private var _photoUrl = photoUrl

    init {
        this.animalRegistrationView.presenter = this
    }

    private var animalName: String? = null
    override fun getAnimalName(): String? {
        return animalName
    }

    override fun setAnimalName(value: String) {
        animalName = value
    }

    private var animalDescription: String? = null
    override fun getAnimalDescription(): String? {
        return animalDescription
    }

    override fun setAnimalDescription(value: String) {
        animalDescription = value
    }

    override fun getImageUri(): String? {
        return this._photoUrl
    }

    override fun setImageUri(imageUri: String?) {
        this._photoUrl = imageUri
    }

    override fun start() {
        if (animalName != null) {
            this.animalRegistrationView.setAnimalName(animalName!!)
        }
        if (animalDescription != null) {
            this.animalRegistrationView.setAnimalDescription(animalDescription!!)
        }
        showImage()
    }

    override fun showImage() {
        this.animalRegistrationView.showImage(this._photoUrl)
    }

    override fun addAnimal(animal: Animal) = runBlocking {
        Log.i(TAG, "register ${animal}")
        animalRepository.saveAnimal(animal)
    }

    override fun makeAnimal(): Animal? {
        if (animalName == null || animalDescription == null || this._photoUrl == null) {
            return null
        }
        val id = Utils.generateUUID()
        val now = Date()
        val today = SimpleDateFormat("yyyy/MM/dd").format(now).toString()
        return Animal(
            id,
            animalName!!,
            animalDescription!!,
            0,
            this._photoUrl!!,
            today
        )
    }

    override fun clearCurrentValues() {
        animalName = null
        animalDescription = null
    }

    override fun logout() = runBlocking {
        withContext(context) {
            loginRepository.logout()
        }
    }
}