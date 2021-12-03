package com.example.aianimals.services.animal.listing

import com.example.aianimals.core.exception.Failure


class AnimalFailure {
    class ListNotAvailable : Failure.FeatureFailure()
    class NonExistentAnimal : Failure.FeatureFailure()
}

