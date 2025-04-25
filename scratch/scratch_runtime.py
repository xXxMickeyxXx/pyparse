def date_lang_main():
	from .scratch_date_lang import date_lang_main
	print()
	date_lang_main()
	print()


def parse_main_main():
	from .scratch_runtime_init import parse_main
	print()
	parse_main()
	print()


def final_redesign_main():
	from .scratch_runtime_init_final_redesign import final_main
	print()
	final_main()
	print()


def main(which=1):
	_runtime_map = {
		1: parse_main_main,
		2: final_redesign_main,
		3: date_lang_main
	}
	return _runtime_map[which]()


if __name__ == "__main__":
	pass
