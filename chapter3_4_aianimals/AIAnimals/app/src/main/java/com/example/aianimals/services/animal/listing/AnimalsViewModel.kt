package com.example.aianimals.services.animal.listing

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.example.aianimals.core.interactor.UseCase
import com.example.aianimals.core.platform.BaseViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject

@HiltViewModel
class AnimalsViewModel
@Inject constructor(private val getAnimals: GetAnimals) : BaseViewModel() {

    private val _animals: MutableLiveData<List<AnimalView>> = MutableLiveData()
    val animals: LiveData<List<AnimalView>> = _animals

    fun loadAnimals() =
        getAnimals(UseCase.None(), viewModelScope) { it.fold(::handleFailure, ::handleAnimalList) }

    private fun handleAnimalList(animals: List<Animal>) {
        _animals.value = animals.map { AnimalView(it.id, it.poster) }
    }
}
