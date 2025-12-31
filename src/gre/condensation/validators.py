import re
from typing import List

from gre.logger.logger import get_logger
from gre.condensation.base import ResponseValidator


REQUIRED_SECTIONS = [
    'Problem_Definition',
    'Taxonomy_or_Approaches',
    'Models_and_Methods',
    'Datasets_and_Benchmarks',
    'Metrics_and_Evaluation',
    'Comparative_Findings',
    'Open_Challenges'
]


class ReviewArticleValidator(ResponseValidator):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)


    def validate(self, response: str) -> bool:
        '''
        Validates that the response contains all required section headers.
        '''
        try:
            missing_sections = []
            for section in REQUIRED_SECTIONS:
                # Check for '### SECTION: <Section_Name>'
                # Using regex to allow for potential slight variations if needed, 
                # but staying strict as per requirement.
                pattern = f'### SECTION: {section}'
                if pattern not in response:
                    missing_sections.append(section)
            
            if missing_sections:
                self.logger.warning(f'Validation failed. Missing sections: {missing_sections}')
                return False
            
            return True
        except Exception as e:
            self.logger.error(f'Validation exception: {e}')
            return False
            

    def clean(self, response: str) -> str:
        '''
        Attempts to clean the response.
        Repairs missing sections by appending them if they are not present.
        '''
        cleaned = response.strip()
        
        # Auto-repair: Check for missing sections and append them
        for section in REQUIRED_SECTIONS:
            pattern = f'### SECTION: {section}'
            if pattern not in cleaned:
                self.logger.warning(f'Repairing response: Appending missing section {section}')
                # Append the section with a placeholder explaining it was empty/missing
                # But per strict format, maybe just the header is enough or header + empty?
                # The prompt says: "If a section has no content, output the section header with no bullets."
                cleaned += f'\n\n{pattern}'
        
        return cleaned
