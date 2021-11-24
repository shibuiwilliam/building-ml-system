package com.example.aianimals.services.animal.listing


import com.example.aianimals.core.exception.Failure
import com.example.aianimals.core.functional.Either
import com.example.aianimals.core.platform.NetworkHandler
import retrofit2.Call
import javax.inject.Inject

interface AnimalsRepository {
    fun animals(): Either<Failure, List<Animal>>
    fun animalDetails(animalId: Int): Either<Failure, AnimalDetails>

    class Network
    @Inject constructor(
        private val networkHandler: NetworkHandler,
        private val service: AnimalsService
    ) : AnimalsRepository {

        override fun animals(): Either<Failure, List<Animal>> {
            return when (networkHandler.isNetworkAvailable()) {
                true -> request(
                    service.animals(),
                    { it.map { animalEntity -> animalEntity.toAnimal() } },
                    emptyList()
                )
                false -> Either.Left(Failure.NetworkConnection)
            }
        }

        override fun animalDetails(animalId: Int): Either<Failure, AnimalDetails> {
            return when (networkHandler.isNetworkAvailable()) {
                true -> request(
                    service.animalDetails(animalId),
                    { it.toAnimalDetails() },
                    AnimalDetailsEntity.empty
                )
                false -> Either.Left(Failure.NetworkConnection)
            }
        }

        private fun <T, R> request(
            call: Call<T>,
            transform: (T) -> R,
            default: T
        ): Either<Failure, R> {
            return try {
                val response = call.execute()
                when (response.isSuccessful) {
                    true -> Either.Right(transform((response.body() ?: default)))
                    false -> Either.Left(Failure.ServerError)
                }
            } catch (exception: Throwable) {
                Either.Left(Failure.ServerError)
            }
        }
    }
}
