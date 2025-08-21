from bs4 import BeautifulSoup


def analyzeSVG(svgFile):
    """
    Analyze and print the complete structure of an SVG file.

    Args:
        svgFile (str): Path to the SVG file
    """

    with open(svgFile, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'xml')

    print("="*80)
    print(f"SVG STRUCTURE ANALYSIS: {svgFile}")
    print("="*80)

    # 1. Root SVG element info
    svgElms = soup.find('svg')
    if svgElms:
        print("\n🎨 ROOT SVG ELEMENT:")
        print("-" * 40)
        for attr, value in svgElms.attrs.items():
            print(f"  {attr}: {value}")

    # 2. All element types in the SVG
    allElms = soup.find_all()
    elmCounts = {}
    for elem in allElms:
        elmCounts[elem.name] = elmCounts.get(elem.name, 0) + 1

    print(f"\n📊 ELEMENT SUMMARY:")
    print("-" * 40)
    for elmType, count in sorted(elmCounts.items()):
        print(f"  {elmType}: {count}")


if __name__ == '__main__':
    svgFile = 'little_tower.svg'
    analyzeSVG(svgFile)
