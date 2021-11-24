package com.example.aianimals.services.animal.listing

import com.example.aianimals.core.interactor.UseCase
import javax.inject.Inject

class GetAnimals
@Inject constructor(private val animalsRepository: AnimalsRepository) : UseCase<List<Animal>, UseCase.None>() {

    override suspend fun run(params: None) = animalsRepository.animals()
}
