import api_calls
import visualize_results
import voice2text
from word2number import w2n


if __name__ == '__main__':
    location, price, room, date = voice2text.run_voice2text()
    room_number = w2n.word_to_num(room)
    # location, price, room, date = "Norflok, Virginia", "300000", "2", "July"
    results = api_calls.get_results(location, ["home", "condo"], room_number, 0,
                                    int(price.replace(",", "") if "," in price else price))
    visualize_results.generate_output(results)
