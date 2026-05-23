import requests
from main import URL_STATS


class CacheLoader:
    def __init__(self, uploaded_files:list) -> requests.models.Response:
        """
        Loads all information for the selected uploaded files from Redis cache.

        :uploaded_files: names of files, which statisitcs is neccessary to get: [img1.png, nature.jpg, ...]
        """
        response = requests.post(URL_STATS, json={"file_names": uploaded_files})
        
        self.response = response
        self.num_img = len(uploaded_files)  # the total number og input images
        self.empty_img_num = None           # total number of empty images
        self.info = None                    # info for all files
        self.status_code = None             # status code of request
        self.unique_species = None          # a set of unique species detected in the files
        self.unique_number = None           # a total number of unuique species detected in the files
        self.species_population = None      # a dictionary for each species population
        self.total_beings_number = None     # a total number of beings detected
        self.average_species_counts = None  # an average distribution of species in images


    def get_status(self) -> int:
        """
        Get status code of http-response

        :returns: status code (e.g. 200, 404, ...)
        """
        if self.status_code is None:
            self.status_code = self.response.status_code
        return self.status_code
    

    def get_dict(self) -> list:
        """
        Transforms json text into python type (a list of dictionaries)

        :returns: a list of statisitcs for the selected files
        """
        if self.info is None:
            self.info = self.response.json()
        return self.info
    

    def get_unique_species(self) -> set[str]:
        """
        Reads all got species on the images and calculates their numbers and types

        :returns: a tuple of (species 1, species 2, ... )
        """

        if self.unique_species is None:

            if self.info is None:
                self.get_dict()

            self.unique_species = set().union(*[d["animals"] for d in self.info])
                
        return self.unique_species


    def get_unique_species_number(self) -> int:
        """
        Calculates the number of unique species detected in all images

        :returns: the number of unique species
        """

        if self.unique_number is None:

            if self.unique_species is None:
                self.get_unique_species()

            self.unique_number = len(self.unique_species)

        return self.unique_number
    

    def get_species_count(self) -> dict[str:int]:
        """
        Calculates total number of each detected species.

        :returns: population info for each species: e.g. {'fox':2, 'boar':3, ...}
        """
        
        if self.species_population is not None:
            return self.species_population
        
        if self.unique_species is None:
            self.get_unique_species
        if self.unique_number is None:
            self.get_unique_species_number()

        self.species_population = dict()

        for animal in self.unique_species:
            self.species_population[animal] = 0

        for img_dict in self.info:
            all_animals = img_dict["animals"]

            for animal, count in all_animals.items():
                self.species_population[animal] += count

        return self.species_population


    def get_total_animals_count(self) -> int:
        """
        Calculates how many animals totally got detected in the files.

        :returns: total number of beings
        """

        if self.species_population is None:
            self.get_species_count()

        self.total_beings_number = 0

        for animal, count in self.species_population.items():
            self.total_beings_number += count


        return self.total_beings_number
    

    def get_top(self, top:int=3) -> tuple[str, int]:
        """
        Reads all detected species destribution and returns top the most popular types.

        :returns: a tuple of the most popular species and their counts.
        """
        if self.species_population is None:
            self.get_species_count()
        if top > self.unique_number:
            raise ValueError("Top of animals is bigger than the whole possible species number")
        
        sorted_counts = sorted(self.species_population.values(), reverse=True)[:top]
        top_species = [(animal, count) for animal, count in self.species_population.items() if count in sorted_counts]
        top_species.sort(reverse=True, key= lambda x: x[1])
        del sorted_counts
        
        return top_species


    def get_av_species_frequency(self, ) -> dict[str:float]:
        """
        Reads species statistics for the selected images and calculates how many times on average
        a distinct species appeared in an image (if it does).

        :returns: a dictionaty how each detected species has been appeared in image (if it does)
        """
        if self.info is None:
            self.get_dict()

        animal_imgcount = dict()        # animal : how many images this animal has been detected in

        if self.average_species_counts is None:
            for img_info in self.info:
                img_animals = img_info["animals"]

                for animal in img_animals.keys():
                    animal_imgcount[animal] = animal_imgcount.get(animal, 0) + 1

        if self.species_population is None:
            self.get_species_count()

        self.average_species_counts = self.species_population.copy()

        for animal in self.average_species_counts.keys():
            self.average_species_counts[animal] /= animal_imgcount[animal]

        del animal_imgcount

        return self.average_species_counts
    

    def get_communal_top(self, top:int=3) -> tuple[str, float]:
        """
        Reads all detected species average destribution and returns top the most communal species (on average).
        The function uses statistics how many beings of each species have been appeared in a distinct images, expressing
        the top most communal species.

        :returns: a tuple of the most communal species and their counts.
        """
        if self.average_species_counts is None:
            self.get_species_count()
        
        if top > self.unique_number:
            raise ValueError("Top of animals is bigger than the whole possible species number")
        
        sorted_counts = sorted(self.average_species_counts.values(), reverse=True)[:top]
        top_species = [(animal, count) for animal, count in self.average_species_counts.items() if count in sorted_counts]
        top_species.sort(reverse=True, key= lambda x: x[1])
        del sorted_counts
        
        return top_species
    

    def get_empty_img(self) -> int:
        """
        Calculates how many images were without detected animals.

        :returns: number of empy images
        """
        if self.empty_img_num is None:

            if self.info is None:
                self.get_dict()

            self.empty_img_num = 0

            for img in self.info:
                all_animals = img["animals"]
                if len(all_animals) == 0:
                    self.empty_img_num += 1

        return self.empty_img_num