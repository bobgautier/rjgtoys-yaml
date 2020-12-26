from rjgtoys.yaml import yaml_dump

data = dict(
    a=1,
    b=2,
    inner=dict(
       part1="part 1",
       part2="part 2",
       items=[1,2,3,4]
    )
)

yaml_dump(data)

