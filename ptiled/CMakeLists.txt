set(PTILED_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/__init__.py
    ${CMAKE_CURRENT_SOURCE_DIR}/math.py
    ${CMAKE_CURRENT_SOURCE_DIR}/resources.py
    ${CMAKE_CURRENT_SOURCE_DIR}/sprite_list.py
    ${CMAKE_CURRENT_SOURCE_DIR}/texture_manager.py
    ${CMAKE_CURRENT_SOURCE_DIR}/types.py
)

if(${INSTALL_PY} MATCHES "ON")
    install(
        FILES
        ${PTILED_FILES}
        DESTINATION ${CMAKE_INSTALL_PREFIX}/ptiled
        PERMISSIONS
        OWNER_READ OWNER_WRITE
        GROUP_READ
        WORLD_READ)

    add_subdirectory(sprite)
    add_subdirectory(tilemap)
endif()
