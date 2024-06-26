# !/usr/bin/python3

# ** info: python imports
import logging

# ** info: typing imports
from typing import Self
from typing import List
from typing import Set

# ** info: dtos imports
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterSearchResponseDto  # type: ignore
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterSearchRequestDto  # type: ignore
from src.modules.parameter.ports.rest_routers_dtos.parameter_dtos import ParameterDataDto  # type: ignore

# ** info: entities imports
from src.modules.parameter.adapters.database_providers_entities.parameter_entity import Parameter  # type: ignore

# ** info: providers imports
from src.modules.parameter.adapters.database_providers.parameter_provider import ParameterProvider  # type: ignore

__all__: list[str] = ["ParameterCore"]


class ParameterCore:
    # !------------------------------------------------------------------------
    # ! info: core slots section start
    # !------------------------------------------------------------------------

    __slots__ = ["_parameter_provider"]

    # !------------------------------------------------------------------------
    # ! info: core atributtes and constructor section start
    # !------------------------------------------------------------------------

    def __init__(self: Self):
        # ** info: providers building
        self._parameter_provider: ParameterProvider = ParameterProvider()

    # !------------------------------------------------------------------------
    # ! info: driver methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from the routers layer
    # ! warning: a method only can be declared in this section if it is going to be called from the routers layer
    # !------------------------------------------------------------------------

    async def driver_search_parameter(self: Self, parameter_search_request: ParameterSearchRequestDto) -> ParameterSearchResponseDto:
        logging.info("starting driver_search_parameter")
        parameters: List[Parameter] = await self._search_by_domain(domain=parameter_search_request.domain)
        parameter_search_response: ParameterSearchResponseDto = await self._map_parameter_response(parameters=parameters)
        logging.info("driver_search_parameter ended")
        return parameter_search_response

    # !------------------------------------------------------------------------
    # ! info: core adapter methods section start
    # ! warning: all the methods in this section are the ones that are going to call methods from another core
    # ! warning: a method only can be declared in this section if it is going to call a port method from another core
    # !------------------------------------------------------------------------

    # !------------------------------------------------------------------------
    # ! info: core port methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from another core
    # ! warning: a method only can be declared in this section if it is going to be called from another core
    # !------------------------------------------------------------------------

    # ** info: cpm pc are initials for core port methods parameter core
    async def cpm_pc_get_set_of_parameter_ids_by_domain(self: Self, domain: str) -> Set[int]:
        logging.info("starting cpm_pc_get_set_of_parameter_ids_by_domain")
        parameters_list: List[Parameter] = self._parameter_provider.search_parameters_by_domain(domain=domain)
        parameters_ids: Set[int] = set([parameter.id for parameter in parameters_list])
        logging.info("cpm_pc_get_set_of_parameter_ids_by_domain ended")
        return parameters_ids

    # !------------------------------------------------------------------------
    # ! info: private class methods section start
    # ! warning: all the methods in this section are the ones that are going to be called from inside this core
    # ! warning: a method only can be declared in this section if it is going to be called from inside this core
    # !------------------------------------------------------------------------

    async def _search_by_domain(self: Self, domain: str) -> List[Parameter]:
        parameters: List[Parameter] = self._parameter_provider.search_parameters_by_domain(domain=domain)
        return parameters

    async def _map_parameter_response(self: Self, parameters: List[Parameter]) -> ParameterSearchResponseDto:
        return ParameterSearchResponseDto(values=await self._map_parameters_data(parameters=parameters))

    async def _map_parameters_data(self: Self, parameters: List[Parameter]) -> List[ParameterDataDto]:
        parameters_data: List[ParameterDataDto] = []
        for parameter in parameters:
            parameter_data: ParameterDataDto = await self._map_parameter_data(parameter=parameter)
            parameters_data.append(parameter_data)
        return parameters_data

    async def _map_parameter_data(self: Self, parameter: Parameter) -> ParameterDataDto:
        return ParameterDataDto(label=parameter.value, value=parameter.id)
