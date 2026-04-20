cmake_minimum_required(VERSION 3.8)
project(amr_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ==============================
# REQUIRED PACKAGES
# ==============================
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# ==============================
# MESSAGE GENERATION
# ==============================
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotPose.msg"
)

# ==============================