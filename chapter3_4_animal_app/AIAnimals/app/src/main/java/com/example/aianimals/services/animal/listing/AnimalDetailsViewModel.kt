package com.example.aianimals.services.animal.listing

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import com.example.aianimals.core.platform.BaseViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject

@HiltViewModel
class AnimalDetailsViewModel
@Inject constructor(
    private val getAnimalDetails: GetAnimalDetails,
) : BaseViewModel() {

    private val _animalDetails: MutableLiveData<AnimalDetailsView> = MutableLiveData()
    val animalDetails: LiveData<AnimalDetailsView> = _animalDetails

    fun loadAnimalDetails(animalId: Int) =
        getAnimalDetails(GetAnimalDetails.Params(animalId), viewModelScope) {
            it.fold(
                ::handleFailure,
                ::handleAnimalDetails
            )
        }

    private fun handleAnimalDetails(animal: AnimalDetails) {
        _animalDetails.value = AnimalDetailsView(
            animal.id, animal.title, animal.poster,
            animal.summary, animal.cast, animal.director, animal.year, animal.trailer
        )
    }
}
