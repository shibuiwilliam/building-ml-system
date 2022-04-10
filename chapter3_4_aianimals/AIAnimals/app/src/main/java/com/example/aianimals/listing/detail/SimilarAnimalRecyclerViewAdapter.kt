package com.example.aianimals.listing.detail

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.aianimals.R
import com.example.aianimals.repository.animal.Animal

class SimilarAnimalRecyclerViewAdapter(
    context: Context,
    animals: Map<String, Animal>,
    presenter: AnimalDetailContract.Presenter
): RecyclerView.Adapter<SimilarAnimalRecyclerViewAdapter.SimilarAnimalRecyclerViewHolder>() {

    var animals: MutableList<Animal> = animals.values.toMutableList()
        set(animals) {
            field = animals
            notifyDataSetChanged()
        }

    private var context: Context = context
    private var presenter = presenter

    private lateinit var onAnimalCellClickListener: OnAnimalCellClickListener

    interface OnAnimalCellClickListener {
        fun onItemClick(animal: Animal)
    }
    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): SimilarAnimalRecyclerViewHolder {
        val inflater = LayoutInflater.from(parent.context)
        val view = inflater.inflate(R.layout.animal_detail_fragment_cell, parent,false)
        return SimilarAnimalRecyclerViewHolder(view)
    }

    override fun onBindViewHolder(holder: SimilarAnimalRecyclerViewHolder, position: Int) {
        val animal = animals[position]
        Glide.with(context).load(animal.imageUrl).into(holder.animalImageView)
        holder.itemView.setOnClickListener{
            onAnimalCellClickListener.onItemClick(animal)
        }
        if (position == animals.size - 1){
            presenter.appendAnimals()
        }
    }

    override fun getItemCount(): Int {
        return animals.size
    }

    inner class SimilarAnimalRecyclerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        var animalImageView: ImageView = itemView.findViewById(R.id.animal_detail_image)
    }

}