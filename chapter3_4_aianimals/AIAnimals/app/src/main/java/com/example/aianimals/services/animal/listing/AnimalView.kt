package com.example.aianimals.services.animal.listing

import android.os.Parcel
import com.example.aianimals.core.platform.KParcelable
import com.example.aianimals.core.platform.parcelableCreator

data class AnimalView(val id: Int, val poster: String) : KParcelable {
    companion object {
        @JvmField
        val CREATOR = parcelableCreator(::AnimalView)
    }

    constructor(parcel: Parcel) : this(parcel.readInt(), parcel.readString()!!)

    override fun writeToParcel(dest: Parcel, flags: Int) {
        with(dest) {
            writeInt(id)
            writeString(poster)
        }
    }
}
