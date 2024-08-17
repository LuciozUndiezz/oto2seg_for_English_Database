from typing import Optional, List, Dict
import json
import re

# Define a type for phoneme map items
EPhonemeMapItem = Dict[str, str]

# Load SAMPA phoneme map from JSON file
with open("./data/arpasing.json", "r", encoding="utf-8") as f:
    sampa_map = json.load(f)

# Define a mapping from ARPAbet to SAMPA
arpabet_to_sampa = {
    "aa": "Q",
    "ae": "{",
    "ah": "@",
    "ao": "O;",
    "aw": "aU",
    "ay": "aI",
    "eh": "e",
    "er": "@r",
    "ey": "eI",
    "ih": "I",
    "iy": "i;",
    "ow": "O;",
    "oy": "OI",
    "uh": "U",
    "uw": "u;",
    "m": "m",
    "n": "n",
    "ng": "N",
    "b": "bh",
    "ch": "tS",
    "d": "dh",
    "dh": "D",
    "dx": "4",
    "f": "f",
    "g": "gh",
    "hh": "h",
    "jh": "dZ",
    "k": "kh",
    "l": "l",
    "p": "ph",
    "r": "r",
    "s": "s",
    "sh": "S",
    "t": "th",
    "th": "T",
    "v": "v",
    "w": "w",
    "y": "j",
    "z": "z",
    "zh": "Z",
}


def convert_arpabet_to_sampa(arpabet_phonemes: List[str]) -> List[str]:
    sampa_phonemes = [
        arpabet_to_sampa.get(phoneme, phoneme) for phoneme in arpabet_phonemes
    ]
    return sampa_phonemes


def convert_oto_to_sampa(oto_phonemes: List[str]) -> List[str]:
    sampa_phonemes = []
    for phoneme in oto_phonemes:
        if phoneme in sampa_map:
            sampa_phonemes.append(sampa_map[phoneme])
        else:
            sampa_phonemes.append(phoneme)  # Fallback to original phoneme
    return sampa_phonemes


def get_sampa_info(sampa: str) -> Optional[EPhonemeMapItem]:
    """Retrieve phoneme information from SAMPA representation."""
    for item in sampa_map:
        if item["sampa"] == sampa:
            return item

    print(f"[Error] SAMPA phoneme '{sampa}' not found in phoneme map.")
    return None

class WarningException(Exception):
    pass


class OtoInfo:
    def __init__(self, alias: str):
        self.alias = alias


class OtoEntryPhonemeInfo:
    def __init__(self):
        self.is_alternative = False
        self.type = None 
        self.phoneme_list = []
        self.phoneme_group = []


class EnglishLanguageTool:
    """Class for processing English phonemes."""

    def __init__(self) -> None:
        # Define the ARPAbet to SAMPA mapping
        self.arpabet_to_sampa = arpabet_to_sampa

        # Load SAMPA phoneme map from JSON file
        with open("./data/arpasing.json", "r", encoding="utf-8") as f:
            self.sampa_map = json.load(f)

        self.vowel_list = [
            "Q",
            "{",
            "V",
            "O;",
            "@",
            "e",
            "@r",
            "I",
            "i;",
            "U",
            "u;",
            "aU",
            "aI",
            "eI",
            "@U",
            "OI",
        ]
        self.syllabic_consonant_list = ["N", "n", "m"]
        self.consonant_list = [
            "bh",
            "dh",
            "tS",
            "D",
            "4",
            "f",
            "gh",
            "h",
            "dZ",
            "kh",
            "l",
            "N",
            "ph",
            "r",
            "s",
            "S",
            "th",
            "T",
            "v",
            "w",
            "j",
            "z",
            "Z",
        ]

        self.alias_vowel_list = [
            "aa",
            "ae",
            "ah",
            "ao",
            "ax",
            "eh",
            "er",
            "ih",
            "iy",
            "uh",
            "uw",
            "aw",
            "ay",
            "ey",
            "ow",
            "oy",
        ]

        self.alias_syllabic_consonant_list = ["n", "ng"]

        self.alias_consonant_list = [
            "b",
            "ch",
            "d",
            "dh",
            "dx",
            "f",
            "g",
            "hh",
            "jh",
            "k",
            "l",
            "m",
            "n",
            "ng",
            "p",
            "q",
            "r",
            "s",
            "sh",
            "t",
            "th",
            "v",
            "w",
            "y",
            "z",
            "zh",
        ]

    def process_phonemes(self, phonemes: List[str], is_alias: bool) -> List[str]:
        sampa_phonemes = []
        for phoneme in phonemes:
            if is_alias:
                # Convert ARPAbet alias to SAMPA
                sampa_phoneme = convert_arpabet_to_sampa(phoneme)
            else:
                # Convert OTO phoneme to SAMPA
                sampa_phoneme = convert_oto_to_sampa(phoneme)
            sampa_phonemes.append(sampa_phoneme)
        return sampa_phonemes

    def get_missing_list(self, phonemes: List[str]) -> List[str]:
        """Returns a list of missing phonemes from the provided list."""

        # Collect all possible phonemes from all lists
        all_phonemes = set(
            self.vowel_list
            + self.syllabic_consonant_list
            + self.consonant_list
            + self.alias_vowel_list
            + self.alias_syllabic_consonant_list
            + self.alias_consonant_list
        )

        # Convert provided phonemes to a set for faster lookup
        phoneme_set = set(phonemes)

        # Identify missing phonemes
        missing_phonemes = list(all_phonemes - phoneme_set)

        return missing_phonemes

        self.cvvc_list = []
        for vowel in self.vowel_list + self.syllabic_consonant_list:
            self.cvvc_list.append(f"Sil {vowel}")
            self.cvvc_list.append(f"{vowel} Sil")
        for consonant in self.consonant_list:
            self.cvvc_list.append(f"Sil {consonant}")
        for consonant in self.consonant_list:
            for vowel in self.vowel_list:
                self.cvvc_list.append(f"{vowel} {consonant}")
                self.cvvc_list.append(f"{consonant} {vowel}")
            for vowel in self.syllabic_consonant_list:
                self.cvvc_list.append(f"{vowel} {consonant}")
        # Deduplicate
        self.cvvc_list = list(set(self.cvvc_list))

    def get_alternative_phoneme(
        self, articulation: str, phoneme_list: List[str]
    ) -> Optional[str]:
        phonemes = articulation.split(" ")

        # Ensure that there are at least two phonemes
        if len(phonemes) < 2:
            print(f"[Warning] Not enough phonemes for articulation '{articulation}'")
            return None

        if (
            self.is_vowel(phonemes[0], True)
            or self.is_syllabic_consonant(phonemes[0], True)
        ) and self.is_consonant(phonemes[1], True):
            vowel = phonemes[0]
            consonant = phonemes[1]
            art_type = "vc"
        elif self.is_consonant(phonemes[0], True) and self.is_vowel(phonemes[1], True):
            vowel = phonemes[1]
            consonant = phonemes[0]
            art_type = "cv"
        elif self.is_consonant(phonemes[0], True):
            vowel = phonemes[1]
            consonant = phonemes[0]
            art_type = "cv"
        elif self.is_consonant(phonemes[1], True):
            vowel = phonemes[0]
            consonant = phonemes[1]
            art_type = "vc"
        else:
            return None

        alt_consonant_list = [consonant]
        alt_vowel_list = [vowel]

        for consonant_list in self.consonant_variant_list:
            if consonant in consonant_list:
                alt_consonant_list.extend(
                    item for item in consonant_list if item not in alt_consonant_list
                )

        for vowel_list in self.vowel_variant_list:
            if vowel in vowel_list:
                alt_vowel_list.extend(
                    item for item in vowel_list if item not in alt_vowel_list
                )

        for alt_consonant in alt_consonant_list:
            for alt_vowel in alt_vowel_list:
                if art_type == "vc":
                    alt_articulation = f"{alt_vowel} {alt_consonant}"
                else:
                    alt_articulation = f"{alt_consonant} {alt_vowel}"

                if alt_articulation in phoneme_list:
                    return alt_articulation

        return None

    def get_phonemes_types(self, phonemes: List[str]) -> List[str]:
        phoneme_types: List[str] = []
        for i in range(len(phonemes) - 1, -1, -1):
            phoneme = phonemes[i]

            if phoneme == "Sil":
                phoneme_types.append("r")
            elif phoneme == "-":
                phoneme_types.append("r")
            elif phoneme in self.vowel_list:
                phoneme_types.append("v")
            elif phoneme in self.syllabic_consonant_list:
                phoneme_types.append("c")
            elif phoneme in self.consonant_list:
                phoneme_types.append("c")
            else:
                phoneme_types.append("?")

        phoneme_types.reverse()
        print(f"[Debug] Phonemes: {phonemes}, Types: {phoneme_types}")

        return phoneme_types

    def get_oto_entry_phoneme_info(self, oto_entry: OtoInfo) -> OtoEntryPhonemeInfo:
        """Returns phoneme info from an OtoInfo object."""
        item_alias = oto_entry.alias
        ret = OtoEntryPhonemeInfo()

        # Check if the alias contains a number and ignore it
        if any(char.isdigit() for char in item_alias):
            print(f"[Info] Numbered alias '{item_alias}' will be ignored.")
            return None

        if re.match(r"[0-9]+$", item_alias):  # Handle alternate phonemes
            ret.is_alternative = True
            item_alias = re.sub(r"[0-9]+$", "", item_alias)

        # Convert ARPAbet to SAMPA
        phonemes = convert_arpabet_to_sampa(item_alias.split())

        phoneme_count = len(phonemes)

        # Replace "-" with "Sil"
        phonemes = ["Sil" if phoneme == "-" else phoneme for phoneme in phonemes]

        # Handle phoneme types
        phoneme_types = self.get_phonemes_types(phonemes)

        # Validate phoneme types length
        if len(phoneme_types) < 2:
            raise WarningException(
                f"[Phoneme Type] Insufficient phoneme types for '{item_alias}'"
            )

        if phoneme_count == 2:        
            
            # Ignore "sil sil" pattern
            
            if phoneme_types[0] == "r" and phoneme_types[1] == "r":
                print(f"[Info] Skipping 'sil sil' pattern for '{item_alias}'")
                return None  
            
                # sil Vowel
            
            elif phoneme_types[0] == "r" and self.is_vowel(phonemes[1], False):
                ret.type = "rv"
                ret.phoneme_group = [phonemes]
                ret.phoneme_list = phonemes     
                
                # vowel vowel
                
            elif phoneme_types[0] == "v" and phoneme_types[1] == "v":
                ret.type = "vv"
                ret.phoneme_group = [phonemes]
                ret.phoneme_list = phonemes
                
                # vowel sil
                
            elif phoneme_types[0] == "v" and phoneme_types[1] == "r":
                ret.type = "vr"
                ret.phoneme_group = [phonemes]
                ret.phoneme_list = phonemes
                
                # consonant vowel
                
            elif phoneme_types[0] == "c" and phoneme_types[1] == "v":
                ret.type = "cv"
                ret.phoneme_group = [phonemes]
                ret.phoneme_list = phonemes
                
                # vowel consonant 
                
            elif phoneme_types[0] == "v" and phoneme_types[1] == "c":
                ret.type = "vc"
                ret.phoneme_group = [phonemes]
                ret.phoneme_list = phonemes
                
                # consonant sil
                
            elif phoneme_types[0] == "c" and phoneme_types[1] == "r":
                ret.type = "cr"
                ret.phoneme_group = [phonemes] 
                
                # consonant consonant
                
            elif phoneme_types[0] == "c" and phoneme_types[1] == "c":
                ret.type = "cc"
                ret.phoneme_group = [phonemes]
                ret.phoneme_list = phonemes
            else:
                raise WarningException(
                    f"[Phoneme Type] Unknown phoneme type for '{item_alias}'"
                )
        else:
            raise WarningException(
                f"[Phoneme Type] Unexpected phoneme count ({phoneme_count}) for '{item_alias}'"
            )

        print(
            f"[Debug] Alias: {oto_entry.alias}, Phonemes: {phonemes}, Type: {ret.type}, Phoneme List: {ret.phoneme_list}"
        )

        return ret


    def is_vowel(self, phoneme: str, is_alias: bool) -> bool:
        return phoneme in (self.alias_vowel_list if is_alias else self.vowel_list)

    def is_syllabic_consonant(self, phoneme: str, is_alias: bool) -> bool:
        return phoneme in (
            self.alias_syllabic_consonant_list
            if is_alias
            else self.syllabic_consonant_list
        )

    def is_consonant(self, phoneme: str, is_alias: bool) -> bool:
        return phoneme in (
            self.alias_consonant_list if is_alias else self.consonant_list
        )


# Initialize the language tool
lang_tool = EnglishLanguageTool()