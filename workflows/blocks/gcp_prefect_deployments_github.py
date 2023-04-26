from prefect.filesystems import GitHub

block = GitHub(
    repository="https://github.com/OlegVolchenko/bikes-rental-project.git",
)
block.save("github")
