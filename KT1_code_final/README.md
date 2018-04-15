# KT_assignment1
dependencies:  
python-pip  
python 2.4 or higher  
git  

Installation instructions:  
- Install dependencies listed above 
- download or clone project directory  
git clone https://github.com/thomasMilesTgm/KT_assignment1  
- run setup.sh from the project root directory
    
# Usage  
basic:
- from run_analysis include run
- run(NGram_distance, NGram_threshold, Neighborhood_distance,Metaphone_neighbors,
                                   Metaphone_nGrams, Metaphone_threshold)


Automated:  
** note: this can take quite some time to run **  
- python ./src/generate_dataset.py                       