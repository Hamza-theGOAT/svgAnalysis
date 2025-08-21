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
    svgElm = soup.find('svg')
    if svgElm:
        print("\n🎨 ROOT SVG ELEMENT:")
        print("-" * 40)
        for attr, value in svgElm.attrs.items():
            print(f"  {attr}: {value}")


if __name__ == '__main__':
    svgFile = 'little_tower.svg'
    analyzeSVG(svgFile)
