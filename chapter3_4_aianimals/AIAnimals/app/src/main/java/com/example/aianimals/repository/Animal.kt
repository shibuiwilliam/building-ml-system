package com.example.aianimals.repository

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.aianimals.middleware.Utils


@Entity(tableName = "animals")
data class Animal @JvmOverloads constructor(
    @PrimaryKey @ColumnInfo(name = "id") var id: String = Utils.generateUUID(),
    @ColumnInfo var name: String = "",
    @ColumnInfo var price: Int = -1,
    @ColumnInfo var date: String = ""
)