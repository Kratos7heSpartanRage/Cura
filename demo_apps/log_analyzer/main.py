from analyzer import analyze_logs

def main():
    result = analyze_logs("data/app.log")
    print(result)

if __name__ == "__main__":
    main()
