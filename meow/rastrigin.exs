Mix.install([
  {:meow, "~> 0.1.0-dev", github: "jonatanklosko/meow", ref: "9a7eb27"},
  {:nx, "~> 0.1.0-dev", github: "elixir-nx/nx", sparse: "nx", ref: "d2f717e", override: true},
  {:exla, "~> 0.1.0-dev", github: "elixir-nx/nx", sparse: "exla", ref: "d2f717e"}
])

Nx.Defn.global_default_options(compiler: EXLA)

if length(System.argv()) != 3 do
  IO.puts("Usage: elixir rastrigin.exs [population_size] [problem_size] [generations]")
  System.halt(1)
end

[population_size, problem_size, generations] = Enum.map(System.argv(), &String.to_integer/1)

defmodule Problem do
  import Nx.Defn

  @two_pi 2 * :math.pi()

  defn evaluate(genomes) do
    (10 + Nx.power(genomes, 2) - 10 * Nx.cos(genomes * @two_pi))
    |> Nx.sum(axes: [1])
    |> Nx.negate()
  end
end

algorithm =
  Meow.objective(&Problem.evaluate/1)
  |> Meow.add_pipeline(
    MeowNx.Ops.init_real_random_uniform(population_size, problem_size, -5.12, 5.12),
    Meow.pipeline([
      MeowNx.Ops.selection_tournament(1.0),
      MeowNx.Ops.crossover_uniform(0.5),
      MeowNx.Ops.mutation_replace_uniform(0.001, -5.12, 5.12),
      MeowNx.Ops.log_best_individual(),
      Meow.Ops.max_generations(generations)
    ])
  )

report = Meow.run(algorithm)

report |> Meow.Report.format_summary() |> IO.puts()
