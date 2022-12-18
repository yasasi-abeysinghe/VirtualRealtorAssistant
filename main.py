import api_calls
import visualize_results


if __name__ == '__main__':
    results = api_calls.get_results("Norfolk Virginia", ["home", "condo"], 1, 0, 300000)
    visualize_results.generate_output(results)
