package com.example.aianimals.listing.listing

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.aianimals.R
import com.example.aianimals.repository.Animal

class AnimalListRecyclerViewAdapter(
    animals: Map<String, Animal>
) : RecyclerView.Adapter<AnimalListRecyclerViewAdapter.AnimalListRecyclerViewHolder>() {
    var animals: List<Animal> = animals.values.toList()
        set(animals) {
            field = animals
            notifyDataSetChanged()
        }

    private lateinit var onAnimalCellClickListener: OnAnimalCellClickListener

    interface OnAnimalCellClickListener {
        fun onItemClick(animal: Animal)
    }

    fun setOnAnimalCellClickListener(onAnimalCellClickListener: OnAnimalCellClickListener) {
        this.onAnimalCellClickListener = onAnimalCellClickListener
    }

    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): AnimalListRecyclerViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        val view = inflater.inflate(R.layout.animal_list_fragment_cell, parent, false)
        return AnimalListRecyclerViewHolder(view)
    }

    override fun onBindViewHolder(holder: AnimalListRecyclerViewHolder, position: Int) {
        val animal = animals[position]
        holder.animalNameView.text = animal.name
        holder.animalLikesView.text = animal.likes.toString()
        holder.animalSubmitDateView.text = animal.date
        holder.itemView.setOnClickListener {
            onAnimalCellClickListener.onItemClick(animal)
        }
    }

    override fun getItemCount(): Int {
        return animals.size
    }

    inner class AnimalListRecyclerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        var animalNameView: TextView
        var animalLikesView: TextView
        var animalSubmitDateView: TextView

        init {
            animalNameView = itemView.findViewById(R.id.animal_name)
            animalLikesView = itemView.findViewById(R.id.animal_likes)
            animalSubmitDateView = itemView.findViewById(R.id.animal_submit_date)
        }
    }
}