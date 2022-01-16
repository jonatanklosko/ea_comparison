Mix.install([
  {:meow, "~> 0.1.0-dev", github: "jonatanklosko/meow", ref: "9a7eb27"},
  {:nx, "~> 0.1.0-dev", github: "elixir-nx/nx", sparse: "nx", ref: "d2f717e", override: true},
  {:exla, "~> 0.1.0-dev", github: "elixir-nx/nx", sparse: "exla", ref: "d2f717e"}
])

Nx.Defn.global_default_options(compiler: EXLA)

if length(System.argv()) != 3 do
  IO.puts("Usage: elixir one_max.exs [population_size] [problem_size] [generations]")
  System.halt(1)
end

[population_size, problem_size, generations] = Enum.map(System.argv(), &String.to_integer/1)

defmodule Problem do
  import Nx.Defn

  defn evaluate(genomes) do
    Nx.sum(genomes, axes: [1])
  end
end

algorithm =
  Meow.objective(&Problem.evaluate/1)
  |> Meow.add_pipeline(
    MeowNx.Ops.init_binary_random_uniform(population_size, problem_size),
    Meow.pipeline([
      MeowNx.Ops.selection_tournament(1.0),
      MeowNx.Ops.crossover_uniform(0.5),
      MeowNx.Ops.mutation_bit_flip(0.001),
      MeowNx.Ops.log_best_individual(),
      Meow.Ops.max_generations(generations)
    ])
  )

report = Meow.run(algorithm)

report |> Meow.Report.format_summary() |> IO.puts()
