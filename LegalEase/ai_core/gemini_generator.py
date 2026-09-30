import os

from dotenv import load_dotenv
from google import genai


load_dotenv(override=True)


class GeminiDocumentGenerator:

    def __init__(self):
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        if not self.demo_mode:
            if not self.api_key:
                raise ValueError(
                    "GEMINI_API_KEY is not configured. "
                    "Please add your Gemini API key to the .env file."
                )

            self.client = genai.Client(
                api_key=self.api_key
            )
        else:
            self.client = None

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        additional_instructions: str = "",
    ) -> str:

        if self.demo_mode:
            return self._generate_demo_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                effective_date=effective_date,
                additional_instructions=additional_instructions,
            )

        prompt = f"""
You are an AI-assisted legal document drafting system.

Create a professional draft legal document based only on the
information supplied by the user.

IMPORTANT RULES:
1. Do not invent names, dates, addresses, amounts, or other facts.
2. If important information is missing, write [NOT PROVIDED].
3. Do not claim that the document is legally enforceable.
4. Do not present the document as legal advice.
5. Use clear and professional legal language.
6. Organize the document with a title, sections, clauses, and
   signature areas where appropriate.
7. Return only the document content.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS:
{terms}

EFFECTIVE DATE:
{effective_date}

ADDITIONAL INSTRUCTIONS:
{additional_instructions or "[NONE]"}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text.strip()

        except Exception as error:
            raise RuntimeError(
                f"Gemini generation failed: {error}"
            ) from error

    def _generate_demo_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
        additional_instructions: str = "",
    ) -> str:

        formatted_terms = []

        for term in terms.split(";"):
            term = term.strip()

            if term:
                formatted_terms.append(
                    f"- {term}"
                )

        terms_text = "\n".join(formatted_terms)

        if not terms_text:
            terms_text = "- [NOT PROVIDED]"

        instructions = (
            additional_instructions.strip()
            if additional_instructions.strip()
            else "[NONE]"
        )

        return f"""LEGAL DOCUMENT DRAFT

DOCUMENT TYPE
{document_type}

EFFECTIVE DATE
{effective_date}

PARTIES
{parties}

TERMS AND CONDITIONS
{terms_text}

ADDITIONAL INSTRUCTIONS
{instructions}

DECLARATION

This document is an AI-generated draft prepared from the
information provided by the user.

IMPORTANT NOTICE

This is a draft document and is not legal advice.
The parties should review the document carefully and obtain
professional legal advice where appropriate.

SIGNATURES

Party 1: ______________________________

Date: _________________________________


Party 2: ______________________________

Date: _________________________________
"""