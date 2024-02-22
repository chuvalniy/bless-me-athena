from typing import Optional, Any, List

import g4f
from langchain.llms.base import LLM
from langchain_core.callbacks import CallbackManagerForLLMRun


class G4F(LLM):
    @property
    def _llm_type(self) -> str:
        return 'custom'

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> str:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo_0613,
            messages=[{"role": "user", "content": prompt}],
        )
        if stop:
            stop_indices = (response.find(s) for s in stop if s in response)
            min_stop = min(stop_indices, default=-1)
            if min_stop > -1:
                response = response[:min_stop]

        return response
