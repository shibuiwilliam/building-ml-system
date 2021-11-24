package com.example.aianimals.services.animal.listing

import com.example.aianimals.core.interactor.UseCase
import javax.inject.Inject

class GetAnimalDetails
@Inject constructor(private val animalsRepository: AnimalsRepository) :
    UseCase<AnimalDetails, GetAnimalDetails.Params>() {

    override suspend fun run(params: Params) = animalsRepository.animalDetails(params.id)

    data class Params(val id: Int)
}
