package com.example.aianimals.repository

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey
import com.example.aianimals.middleware.Utils


@Entity(tableName = "animals")
data class Animal @JvmOverloads constructor(
    @PrimaryKey @ColumnInfo(name = "id") var id: String = Utils.generateUUID(),
    @ColumnInfo var name: String = "",
    @ColumnInfo var description: String = "",
    @ColumnInfo var date: String = "",
    @ColumnInfo var likes: Int = 0,
    @ColumnInfo var imageUrl: String = "https://www.anicom-sompo.co.jp/nekonoshiori/wp-content/uploads/2018/12/724-2.jpg"
)