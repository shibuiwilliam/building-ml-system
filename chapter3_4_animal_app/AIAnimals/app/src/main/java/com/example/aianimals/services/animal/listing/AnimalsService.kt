package com.example.aianimals.services.animal.listing

import retrofit2.Retrofit
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class AnimalsService
@Inject constructor(retrofit: Retrofit) : AnimalsApi {
    private val animalsApi by lazy { retrofit.create(AnimalsApi::class.java) }

    override fun animals() = animalsApi.animals()
    override fun animalDetails(animalId: Int) = animalsApi.animalDetails(animalId)
}
